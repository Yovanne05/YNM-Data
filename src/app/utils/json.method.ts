export function getObjectKeys(obj: Record<string, unknown>): string[] {
    return Object.keys(obj);
}

export function getValue(key: string, item: Record<string, unknown>): unknown {
    return item?.[key] ?? null;
}
