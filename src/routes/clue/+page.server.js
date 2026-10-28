// @ts-ignore
export async function load({ fetch }) {
    try {
        const userId = 1; // จำลอง User ID
        const res = await fetch(`http://127.0.0.1:8000/collections/by-user/${userId}`);
        
        if (!res.ok) {
            return { target: null };
        }
        
        const collections = await res.json();
        
        // กรองเฉพาะรายการที่ยังล็อกอยู่ (is_locked = true)
        // @ts-ignore
        const lockedItems = collections.filter(item => item.is_locked);
        
        if (lockedItems.length === 0) {
            return { target: null, completed: true }; // ปลดล็อกครบทุกชิ้นแล้ว
        }
        
        // สุ่มดึงเป้าหมาย 1 ชิ้นจากรายการที่ยังล็อกอยู่
        const randomTarget = lockedItems[Math.floor(Math.random() * lockedItems.length)];
        
        return { target: randomTarget, completed: false };
    } catch (error) {
        console.error("Fetch clue error:", error);
        return { target: null, completed: false };
    }
}