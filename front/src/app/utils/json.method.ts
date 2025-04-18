export function getObjectKeys(obj: Record<string, unknown>): string[] {
    return Object.keys(obj);
}

export function getValue(key: string, item: Record<string, unknown>): unknown {
    if (key.toLowerCase().includes('date') && typeof item?.[key] == "string") {
        let date:string = item?.[key] as string;
        return new Date(date).toISOString().split("T")[0];
    }
    return item?.[key] ?? null;
}
