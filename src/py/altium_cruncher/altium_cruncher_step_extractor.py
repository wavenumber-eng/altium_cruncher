"""
Altium 3D Model Extractor

Extract 3D model files (STEP, SLDPRT, Parasolid, etc.) from Altium PcbDoc and PcbLib files.

Altium stores 3D models in the Models/ section of the OLE/CFB container,
compressed with zlib. This module extracts and decompresses them.

Supported formats:
  - STEP (.step/.stp) - ISO-10303-21 format
  - SLDPRT (.SLDPRT/.SLDASM) - SolidWorks part/assembly files
  - Parasolid (.x_t/.x_b) - Parasolid text/binary formats

Example:
    from altium_cruncher.altium_cruncher_step_extractor import extract_step_models_from_pcbdoc

    models = extract_step_models_from_pcbdoc(
        Path("design.PcbDoc"),
        Path("output/models/"),
        verbose=True
    )
"""

import logging
import re
import zlib
from pathlib import Path

from altium_monkey.altium_ole import AltiumOleFile

log = logging.getLogger(__name__)

def _extract_model_metadata(ole: AltiumOleFile, stream_prefix: list[str], model_index: int = 0) -> str | None:
    """
    Extract model name from Models/Data metadata stream for a specific model index.

    Altium stores model metadata in the Models/Data stream with format:
    <length>EMBED=TRUE|MODELSOURCE=...|NAME=filename.ext|...

    Multiple models are stored sequentially in the same stream.

    Args:
        ole: Open AltiumOleFile object
        stream_prefix: Stream prefix (e.g., ['Models'] for PcbDoc or ['Library', 'Models'] for PcbLib)
        model_index: Index of the model to extract metadata for (0-based)

    Returns:
        Model filename from NAME= field, or None if not found

    Example:
        >>> _extract_model_metadata(ole, ['Models'], 0)
        'RESC1005X04L.step'
        >>> _extract_model_metadata(ole, ['Models'], 1)
        'GT-USB-7010C.SLDPRT'
    """
    try:
        data_stream = stream_prefix + ['Data']
        if ole.exists(data_stream):
            data = ole.openstream(data_stream)
            # Decode as ASCII/UTF-8 (ignore errors)
            text = data.decode('utf-8', errors='ignore')
            # Find all NAME=filename patterns
            pattern = r'NAME=([^|\x00]+)'
            matches = re.findall(pattern, text)
            if model_index < len(matches):
                return matches[model_index].strip()
    except Exception:
        pass
    return None

def _extract_step_model_name(step_data: bytes) -> str | None:
    """
    Extract the model name from STEP file PRODUCT record.

    Searches for: PRODUCT('ModelName.step','ModelName.step',...)
    or: PRODUCT ( 'ModelName', 'ModelName', ...)

    Args:
        step_data: Raw STEP file content

    Returns:
        Model name without extension, or None if not found

    Example:
        >>> data = b"#7 = PRODUCT('RESC2012X07L.step','RESC2012X07L.step'..."
        >>> _extract_step_model_name(data)
        'RESC2012X07L'
    """
    try:
        # Decode as text (STEP files are ASCII)
        text = step_data.decode('utf-8', errors='ignore')

        # Find PRODUCT record: PRODUCT('name','name',...)
        # Pattern matches: PRODUCT('ModelName') or PRODUCT ( 'ModelName', ...)
        # With optional spaces around parentheses
        pattern = r"PRODUCT\s*\(\s*'([^']+)'"
        match = re.search(pattern, text)

        if match:
            name = match.group(1)
            # Remove .step extension if present
            if name.lower().endswith('.step'):
                name = name[:-5]
            # Remove .stp extension if present
            elif name.lower().endswith('.stp'):
                name = name[:-4]

            # Sanitize filename (remove invalid characters)
            # Replace path separators and other problematic chars
            name = name.replace('/', '_').replace('\\', '_').replace(':', '_')

            return name

    except Exception:
        # If parsing fails, return None
        pass

    return None

def extract_step_models_from_pcbdoc(
    pcbdoc_path: Path,
    output_dir: Path,
    verbose: bool = False
) -> list[Path]:
    """
    Extract all STEP model files from an Altium PcbDoc file.

    3D models are stored in the Models/ section of the OLE container:
        Models/0, Models/1, Models/2, etc.

    The data is zlib-compressed and must be decompressed before saving.

    Args:
        pcbdoc_path: Path to .PcbDoc file
        output_dir: Directory to save extracted STEP files
        verbose: If True, print detailed extraction progress

    Returns:
        List of paths to extracted STEP files

    Example:
        extracted = extract_step_models_from_pcbdoc(
            Path("project.PcbDoc"),
            Path("project_models/")
        )
        log.info(f"Extracted {len(extracted)} models")
    """
    pcbdoc_path = Path(pcbdoc_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not pcbdoc_path.exists():
        raise FileNotFoundError(f"PcbDoc not found: {pcbdoc_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        log.info("")
        log.info("="*80)
        log.info(f"Extracting STEP Models: {pcbdoc_path.name}")
        log.info("="*80)
        log.info("")

    ole = AltiumOleFile(str(pcbdoc_path))
    extracted_files = []
    seen_hashes = {}  # Track content hashes to deduplicate identical models

    # Extract Models/0, Models/1, Models/2, etc.
    model_index = 0
    skipped_duplicates = 0

    while True:
        model_stream = ['Models', str(model_index)]

        if not ole.exists(model_stream):
            break  # No more models

        # Read compressed model data
        compressed_data = ole.openstream(model_stream)

        if verbose:
            log.info(f"Models/{model_index}: {len(compressed_data):,} bytes (compressed)")

        # Decompress (models are zlib-compressed)
        if compressed_data.startswith(b'\x78\x9c'):  # zlib magic bytes
            try:
                decompressed_data = zlib.decompress(compressed_data)
                if verbose:
                    log.info(f"  Decompressed: {len(decompressed_data):,} bytes")
            except Exception as e:
                if verbose:
                    log.warning(f"  Failed to decompress: {e}")
                model_index += 1
                continue
        else:
            # Not compressed
            decompressed_data = compressed_data
            if verbose:
                log.warning("  Not compressed (unusual)")

        # Detect file type and extract
        import hashlib
        content_hash = hashlib.sha256(decompressed_data).hexdigest()

        # Check if we've already extracted this exact model
        if content_hash in seen_hashes:
            skipped_duplicates += 1
            if verbose:
                existing_file = seen_hashes[content_hash]
                log.info(f"  [SKIP] Duplicate of {existing_file.name}")
            model_index += 1
            continue

        # Try to get model name from metadata first (pass model_index)
        metadata_name = _extract_model_metadata(ole, ['Models'], model_index)

        model_name = None
        file_extension = None

        if metadata_name:
            # Use metadata filename - trust the extension
            if '.' in metadata_name:
                parts = metadata_name.rsplit('.', 1)
                model_name = parts[0]
                file_extension = '.' + parts[1]  # Preserve original case
            else:
                model_name = metadata_name
                file_extension = '.dat'  # Fallback if no extension in metadata

            if verbose:
                log.info(f"  Model: {model_name}{file_extension}")

        else:
            # No metadata - try to detect format and extract name
            is_step = decompressed_data.startswith(b'ISO-10303-21;')

            if is_step:
                file_extension = '.step'
                # Try to extract name from PRODUCT record
                model_name = _extract_step_model_name(decompressed_data)

                if verbose:
                    if model_name:
                        log.info(f"  STEP model (from content): {model_name}{file_extension}")
                    else:
                        log.info("  STEP model detected")
            else:
                # Unknown format, no metadata
                file_extension = '.dat'
                if verbose:
                    log.warning("  Unknown format (no metadata)")
                    log.info(f"    Header: {decompressed_data[:32].hex()}")

        # Determine output filename
        if model_name:
            filename = f"{model_name}{file_extension}"
        elif metadata_name:
            filename = metadata_name
        else:
            filename = f"model_{model_index}{file_extension}"

        output_file = output_dir / filename

        # Check if file exists and has the same content (deduplication across runs)
        skip_this_model = False
        if output_file.exists():
            try:
                existing_data = output_file.read_bytes()
                existing_hash = hashlib.sha256(existing_data).hexdigest()

                if existing_hash == content_hash:
                    # Same content, skip this file
                    skipped_duplicates += 1
                    if verbose:
                        log.info(f"  [SKIP] Already extracted: {filename}")
                    skip_this_model = True
            except Exception:
                pass  # If can't read existing file, proceed with extraction

        if skip_this_model:
            # Still track the file even though we skipped it
            extracted_files.append(output_file)
            seen_hashes[content_hash] = output_file
            model_index += 1
            continue

        # If filename conflicts with different content, add suffix
        suffix = 1
        base_name = model_name if model_name else f"model_{model_index}"
        while output_file.exists():
            try:
                existing_data = output_file.read_bytes()
                existing_hash = hashlib.sha256(existing_data).hexdigest()
                if existing_hash == content_hash:
                    # Found duplicate with suffix, skip
                    skipped_duplicates += 1
                    if verbose:
                        log.info(f"  [SKIP] Already extracted as: {output_file.name}")
                    skip_this_model = True
                    break
            except Exception:
                pass

            # Different content, try next suffix
            filename = f"{base_name}_{suffix}{file_extension}"
            output_file = output_dir / filename
            suffix += 1

        if skip_this_model:
            # Still track the file even though we skipped it
            extracted_files.append(output_file)
            seen_hashes[content_hash] = output_file
            model_index += 1
            continue

        # Save the file
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)

        # Track this model by content hash
        seen_hashes[content_hash] = output_file

        if verbose:
            log.info(f"  Saved: {output_file.name}")

        extracted_files.append(output_file)

        model_index += 1

    ole.close()

    if verbose:
        log.info("")
        log.info("="*80)
        log.info("Summary")
        log.info("="*80)
        if extracted_files:
            log.info(f"Extracted {len(extracted_files)} model(s)")
            for f in extracted_files:
                log.info(f"  - {f.name}")
        else:
            log.warning("No models found in PcbDoc")
        log.info(f"Output directory: {output_dir}")
        log.info("")

    return extracted_files

def extract_step_models_from_pcblib(
    pcblib_path: Path,
    output_dir: Path,
    verbose: bool = False
) -> list[Path]:
    """
    Extract all 3D model files from an Altium PcbLib file.

    PcbLib files store 3D models in the Library/Models/ section:
        Library/Models/0, Library/Models/1, etc.

    Args:
        pcblib_path: Path to .PcbLib file
        output_dir: Directory to save extracted model files
        verbose: If True, print detailed extraction progress

    Returns:
        List of paths to extracted model files

    Example:
        extracted = extract_step_models_from_pcblib(
            Path("footprint.PcbLib"),
            Path("models/")
        )
        log.info(f"Extracted {len(extracted)} models")
    """
    pcblib_path = Path(pcblib_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not pcblib_path.exists():
        raise FileNotFoundError(f"PcbLib not found: {pcblib_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        log.info("")
        log.info("="*80)
        log.info(f"Extracting 3D Models: {pcblib_path.name}")
        log.info("="*80)
        log.info("")

    ole = AltiumOleFile(str(pcblib_path))
    extracted_files = []
    seen_hashes = {}
    skipped_duplicates = 0

    # Extract Library/Models/0, Library/Models/1, etc.
    model_index = 0

    while True:
        model_stream = ['Library', 'Models', str(model_index)]

        if not ole.exists(model_stream):
            break  # No more models

        # Read compressed model data
        compressed_data = ole.openstream(model_stream)

        if verbose:
            log.info(f"Library/Models/{model_index}: {len(compressed_data):,} bytes (compressed)")

        # Decompress (models are zlib-compressed)
        if compressed_data.startswith(b'\x78\x9c'):  # zlib magic bytes
            try:
                decompressed_data = zlib.decompress(compressed_data)
                if verbose:
                    log.info(f"  Decompressed: {len(decompressed_data):,} bytes")
            except Exception as e:
                if verbose:
                    log.warning(f"  Failed to decompress: {e}")
                model_index += 1
                continue
        else:
            # Not compressed
            decompressed_data = compressed_data
            if verbose:
                log.warning("  Not compressed (unusual)")

        # Detect file type and extract
        import hashlib
        content_hash = hashlib.sha256(decompressed_data).hexdigest()

        # Check if we've already extracted this exact model
        if content_hash in seen_hashes:
            skipped_duplicates += 1
            if verbose:
                existing_file = seen_hashes[content_hash]
                log.info(f"  [SKIP] Duplicate of {existing_file.name}")
            model_index += 1
            continue

        # Try to get model name from metadata first (PcbLib uses Library/Models/Data, pass model_index)
        metadata_name = _extract_model_metadata(ole, ['Library', 'Models'], model_index)

        model_name = None
        file_extension = None

        if metadata_name:
            # Use metadata filename - trust the extension
            if '.' in metadata_name:
                parts = metadata_name.rsplit('.', 1)
                model_name = parts[0]
                file_extension = '.' + parts[1]  # Preserve original case
            else:
                model_name = metadata_name
                file_extension = '.dat'  # Fallback if no extension in metadata

            if verbose:
                log.info(f"  Model: {model_name}{file_extension}")

        else:
            # No metadata - try to detect format and extract name
            is_step = decompressed_data.startswith(b'ISO-10303-21;')

            if is_step:
                file_extension = '.step'
                # Try to extract name from PRODUCT record
                model_name = _extract_step_model_name(decompressed_data)

                if verbose:
                    if model_name:
                        log.info(f"  STEP model (from content): {model_name}{file_extension}")
                    else:
                        log.info("  STEP model detected")
            else:
                # Unknown format, no metadata
                file_extension = '.dat'
                if verbose:
                    log.warning("  Unknown format (no metadata)")
                    log.info(f"    Header: {decompressed_data[:32].hex()}")

        # Determine output filename
        if model_name:
            filename = f"{model_name}{file_extension}"
        elif metadata_name:
            filename = metadata_name
        else:
            filename = f"model_{model_index}{file_extension}"

        output_file = output_dir / filename

        # Check if file exists and has the same content (deduplication across runs)
        skip_this_model = False
        if output_file.exists():
            try:
                existing_data = output_file.read_bytes()
                existing_hash = hashlib.sha256(existing_data).hexdigest()

                if existing_hash == content_hash:
                    # Same content, skip this file
                    skipped_duplicates += 1
                    if verbose:
                        log.info(f"  [SKIP] Already extracted: {filename}")
                    skip_this_model = True
            except Exception:
                pass  # If can't read existing file, proceed with extraction

        if skip_this_model:
            # Still track the file even though we skipped it
            extracted_files.append(output_file)
            seen_hashes[content_hash] = output_file
            model_index += 1
            continue

        # If filename conflicts with different content, add suffix
        suffix = 1
        base_name = model_name if model_name else f"model_{model_index}"
        while output_file.exists():
            try:
                existing_data = output_file.read_bytes()
                existing_hash = hashlib.sha256(existing_data).hexdigest()
                if existing_hash == content_hash:
                    # Found duplicate with suffix, skip
                    skipped_duplicates += 1
                    if verbose:
                        log.info(f"  [SKIP] Already extracted as: {output_file.name}")
                    skip_this_model = True
                    break
            except Exception:
                pass

            # Different content, try next suffix
            filename = f"{base_name}_{suffix}{file_extension}"
            output_file = output_dir / filename
            suffix += 1

        if skip_this_model:
            # Still track the file even though we skipped it
            extracted_files.append(output_file)
            seen_hashes[content_hash] = output_file
            model_index += 1
            continue

        # Save the file
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)

        # Track this model by content hash
        seen_hashes[content_hash] = output_file

        if verbose:
            log.info(f"  Saved: {output_file.name}")

        extracted_files.append(output_file)

        model_index += 1

    ole.close()

    if verbose:
        log.info("")
        log.info("="*80)
        log.info("Summary")
        log.info("="*80)
        if extracted_files:
            log.info(f"Extracted {len(extracted_files)} model(s)")
            for f in extracted_files:
                log.info(f"  - {f.name}")
        else:
            log.warning("No models found in PcbLib")
        log.info(f"Output directory: {output_dir}")
        log.info("")

    return extracted_files

def extract_step_models_with_component_names(
    pcbdoc_path: Path,
    output_dir: Path,
    verbose: bool = False
) -> list[Path]:
    """
    Extract STEP models with component-based filenames.

    This function reads the Components6/Data stream to map models
    to component footprints, providing more meaningful filenames.

    Args:
        pcbdoc_path: Path to .PcbDoc file
        output_dir: Directory to save extracted STEP files
        verbose: If True, print detailed extraction progress

    Returns:
        List of paths to extracted STEP files

    Note:
        This is a more advanced version that requires parsing component
        data to map model indices to footprint names. For simple extraction,
        use extract_step_models_from_pcbdoc().

    Example:
        extracted = extract_step_models_with_component_names(
            Path("project.PcbDoc"),
            Path("project_models/")
        )
    """
    # TODO: Parse Components6/Data to get footprint -> model index mapping
    # TODO: Use footprint names for output filenames
    # For now, fall back to simple extraction
    log.warning("Component-based naming not implemented yet, using model_N.step")
    return extract_step_models_from_pcbdoc(pcbdoc_path, output_dir, verbose)
