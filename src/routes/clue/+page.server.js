// @ts-ignore
export async function load({ fetch }) {
    try {
        const userId = 1;
        const res = await fetch(`http://127.0.0.1:8000/clue/target/${userId}`);
        
        if (!res.ok) {
            return { target: null };
        }
        
        const data = await res.json();
       
        return { target: data };
    } catch (error) {
        console.error("Fetch clue error:", error);
        return { target: null };
    }
}