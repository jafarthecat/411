export const actions = {
    // @ts-ignore
    submitCode: async ({ request, fetch }) => {
        const data = await request.formData();
        const code = data.get('artifact_code');
        const userId = 1; // จำลอง User ID

        try {
            const res = await fetch('http://127.0.0.1:8000/collections/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, qr_code_val: code })
            });

            if (!res.ok) {
                const errorData = await res.json();
                return { success: false, message: `“ยังเปิดผนึกไม่ได้: ${errorData.detail || 'รหัสนี้ไม่ถูกต้อง หรือวัตถุชิ้นนี้อยู่ในคอลเลกชันแล้ว'}”` };
            }

            const result = await res.json();
            return { success: true, message: `“ยืนยันการค้นพบแล้ว! ${result.item.name} ถูกเพิ่มลงในคอลเลกชันของคุณ”` };
            
        } catch (error) {
            return { success: false, message: '“ระบบบันทึกหลักฐานยังไม่ตอบสนอง โปรดลองอีกครั้งในอีกสักครู่”' };
        }
    }
};
