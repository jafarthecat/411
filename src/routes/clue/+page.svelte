<script>
    let { data } = $props();
</script>

<main>
    <!-- 1. Check if user hasn't completed the quiz / drawn fate -->
    {#if !data.target || !data.target.has_quiz}
        <div class="locked-box" style="text-align: center; padding: 50px 20px;">
            <div style="font-size: 48px; margin-bottom: 12px;">🔒</div>
            <h2>ยังเปิดแฟ้มคำใบ้ไม่ได้</h2>
            <p style="color: #aaa; margin-bottom: 20px;">
                “นักสำรวจทุกคนต้องมีจุดเริ่มต้นก่อน ทำแบบทดสอบหรือสุ่มชะตาเพื่อรับวัตถุโบราณชิ้นแรก แล้วฉันจะมอบเบาะแสให้”
            </p>
            <a href="/quiz" class="gold-btn" style="display: inline-block; background: #ccad4c; color: #14120b; padding: 12px 24px; border-radius: 6px; font-weight: bold; text-decoration: none;">
                รับวัตถุโบราณเริ่มต้น →
            </a>
        </div>

    <!-- 2. Check if all 16 items have been collected -->
    {:else if data.target.completed}
        <div class="completed-box" style="text-align: center; padding: 50px 20px;">
            <div style="font-size: 48px; margin-bottom: 12px;">🏆</div>
            <h2>ภารกิจสำเร็จแล้ว!</h2>
            <p style="color: #aaa;">“คุณตามรอยจนครบทุกชิ้นแล้ว พิพิธภัณฑ์ขอจารึกชื่อคุณไว้ในฐานะนักสำรวจผู้ไม่ยอมแพ้”</p>
        </div>

    <!-- 3. Show current target clue for active players -->
    {:else}
        <div class="clue-container">
            <p class="eyebrow" style="color: #ccad4c; font-size: 12px; letter-spacing: 2px;">แฟ้มภารกิจ · เป้าหมายถัดไป</p>
            <p style="color: #aaa; text-align: center;">“เบาะแสชิ้นใหม่มาแล้ว อ่านให้ดี แล้วออกตามหาวัตถุที่ซ่อนอยู่ในห้องจัดแสดง”</p>
            
            <div class="card" style="border: 2px dashed #ccad4c; padding: 30px; border-radius: 12px; text-align: center; margin: 20px 0;">
                <div class="question-mark" style="font-size: 36px; color: #ff4d4d; font-weight: bold;">?</div>
                <p style="color: #ccc; margin-top: 10px;">เสียงกระซิบจากอดีต</p>
                <h2 style="font-size: 20px; font-style: italic; margin: 15px 0;">"{data.target.clue_text}"</h2>
                <p style="color: #ccad4c;">
                    Gallery: {data.target.gallery_name} (Room {data.target.room_no})
                </p>
            </div>

            <a href="/unlock" class="gold-btn" style="display: block; width: 100%; text-align: center; background: #ccad4c; color: #14120b; padding: 14px; border-radius: 6px; font-weight: bold; text-decoration: none;">
                พบแล้ว! กรอกรหัสเพื่อเปิดผนึก →
            </a>
        </div>
    {/if}
</main>
