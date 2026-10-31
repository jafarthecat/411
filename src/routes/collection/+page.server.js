// @ts-ignore
export async function load({ fetch }) {
    try {
        const userId = 1;
        const res = await fetch(`http://127.0.0.1:8000/collections/by-user/${userId}`);
        
        if (!res.ok) {
            return { collections: [] };
        }
        
        const collections = await res.json();
        return { collections };
    } catch (error) {
        console.error("Fetch collections error:", error);
        return { collections: [] };
    }
}