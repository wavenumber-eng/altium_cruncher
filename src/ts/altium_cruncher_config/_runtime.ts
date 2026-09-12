/** Finite JSON transport shared by the generated config validators. */
export function assertJsonValue(value: unknown, parents: Set<object>): void {
  if (value === null || typeof value === "string" || typeof value === "boolean") return;
  if (typeof value === "number" && Number.isFinite(value)) return;
  if (typeof value !== "object" || value === null || parents.has(value)) {
    throw new Error("Config must contain finite JSON values");
  }
  if (!Array.isArray(value) && ![Object.prototype, null].includes(Object.getPrototypeOf(value))) {
    throw new Error("Config must contain JSON objects");
  }
  parents.add(value);
  if (Array.isArray(value)) {
    for (const item of value) assertJsonValue(item, parents);
  } else {
    for (const key of Reflect.ownKeys(value)) {
      if (typeof key !== "string") throw new Error("Config keys must be strings");
      assertJsonValue((value as Record<string, unknown>)[key], parents);
    }
  }
  parents.delete(value);
}


export function decodeConfig<T>(value: unknown, validate: {
  (value: unknown): value is T;
  errors: {instancePath: string; message?: string}[] | null;
}, label: string): T {
  assertJsonValue(value, new Set());
  if (!validate(value)) {
    const message = validate.errors?.map((error) => `${error.instancePath || "/"}: ${error.message}`).join("; ");
    throw new Error(`Invalid ${label} config: ${message}`);
  }
  return structuredClone(value);
}
