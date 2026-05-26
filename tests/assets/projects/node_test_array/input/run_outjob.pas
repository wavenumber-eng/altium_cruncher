//******************************************************************************
//  Auto-generated OutJob runner
//******************************************************************************

var
    LogFile    : TextFile;
    ErrorCount : Integer;
    Workspace  : IWorkspace;
    Project    : IProject;
    OutJobDoc  : Variant;

procedure Log(Msg : String);
begin
    WriteLn(LogFile, FormatDateTime('hh:nn:ss', Now) + ' ' + Msg);
    Flush(LogFile);
end;

procedure WriteMarker(Path : String; Content : String);
var
    F : TextFile;
begin
    AssignFile(F, Path);
    Rewrite(F);
    Write(F, Content);
    CloseFile(F);
end;

procedure RunOutJob(ProjectPath : String; OutJobPath : String);
begin
    if Not FileExists(ProjectPath) then
    begin
        Log('ERROR: Project not found: ' + ProjectPath);
        Inc(ErrorCount);
        Exit;
    end;

    if Not FileExists(OutJobPath) then
    begin
        Log('ERROR: OutJob not found: ' + OutJobPath);
        Inc(ErrorCount);
        Exit;
    end;

    Log('Opening project: ' + ProjectPath);
    ResetParameters;
    AddStringParameter('ObjectKind', 'Project');
    AddStringParameter('FileName', ProjectPath);
    RunProcess('WorkspaceManager:OpenObject');
    Sleep(1000);
    Application.ProcessMessages;

    Workspace := GetWorkspace;
    if Workspace = Nil then
    begin
        Log('ERROR: GetWorkspace returned nil');
        Inc(ErrorCount);
        Exit;
    end;

    Project := Workspace.DM_FocusedProject;
    if Project = Nil then
    begin
        Log('ERROR: No focused project');
        Inc(ErrorCount);
        Exit;
    end;

    Log('Compiling project');
    Project.DM_Compile;
    Sleep(500);
    Application.ProcessMessages;

    Log('Opening OutJob: ' + OutJobPath);
    OutJobDoc := Client.OpenDocument('OUTPUTJOB', OutJobPath);
    if OutJobDoc = Nil then
    begin
        Log('ERROR: Could not open OutJob');
        Inc(ErrorCount);
        Exit;
    end;

    Client.ShowDocument(OutJobDoc);
    Sleep(500);
    Application.ProcessMessages;

    Log('Running GenerateReport');
    ResetParameters;
    AddStringParameter('ObjectKind', 'OutputBatch');
    AddStringParameter('Action', 'Run');
    RunProcess('WorkSpaceManager:GenerateReport');
    Sleep(1000);
    Application.ProcessMessages;

    Log('OutJob run completed');

    if OutJobDoc <> Nil then
    begin
        Client.CloseDocument(OutJobDoc);
        Log('Closed OutJob document');
    end;

    // Close all project docs to avoid accumulation during batch runs.
    ResetParameters;
    AddStringParameter('ObjectKind', 'FocusedProjectDocuments');
    RunProcess('WorkspaceManager:CloseObject');
    Sleep(300);
    Application.ProcessMessages;

    ResetParameters;
    AddStringParameter('ObjectKind', 'FocusedProject');
    RunProcess('WorkspaceManager:CloseObject');
    Sleep(300);
    Application.ProcessMessages;
end;

procedure Run;
begin
    ErrorCount := 0;
    AssignFile(LogFile, 'C:\eli\wn_pcb\tools\altium\tests\common\real_world\node_test_array\input\run_outjob.log');
    Rewrite(LogFile);

    try
        Log('Script started');
        RunOutJob('C:\eli\wn_pcb\tools\altium\tests\common\real_world\node_test_array\input\11-10077__node-test-array__B4.PrjPcb', 'C:\eli\wn_pcb\tools\altium\tests\common\real_world\node_test_array\input\reference_gen.OutJob');
    except
        Log('ERROR: Unhandled exception in Run');
        Inc(ErrorCount);
    end;

    // Close log + marker before attempting to close this script project.
    WriteMarker('C:\eli\wn_pcb\tools\altium\tests\common\real_world\node_test_array\input\run_outjob.done', 'DONE:' + IntToStr(ErrorCount));
    CloseFile(LogFile);

    // Best-effort: close script project from workspace so repeated runs do not
    // accumulate multiple run_outjob.PrjScr entries.
    ResetParameters;
    AddStringParameter('ObjectKind', 'Project');
    AddStringParameter('FileName', 'C:\eli\wn_pcb\tools\altium\tests\common\real_world\node_test_array\input\run_outjob.PrjScr');
    RunProcess('WorkspaceManager:CloseObject');
end;

end.
