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
                return { success: false, message: errorData.detail || 'รหัสไม่ถูกต้อง หรือคุณปลดล็อกไปแล้ว' };
            }

            const result = await res.json();
            return { success: true, message: `ปลดล็อกสำเร็จ! คุณได้รับ: ${result.item.name}` };
            
        } catch (error) {
            return { success: false, message: 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้' };
        }
    }
};