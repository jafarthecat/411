<script>
    let { data } = $props();
    let target = $derived(data.target);
    let completed = $derived(data.completed);
</script>

<div class="clue-container">
    <h2>Current Target</h2>
    
    {#if completed}
        <div class="target-card">
            <div class="icon">🎉</div>
            <h3>ยินดีด้วย!</h3>
            <p class="clue-text">คุณรวบรวม Artifact ทั้งหมดในพิพิธภัณฑ์ครบแล้ว!</p>
        </div>
        <a href="/collection" class="action-btn">ไปดูคอลเลกชันของคุณ</a>
    {:else if target}
        <div class="target-card">
            <div class="icon">❓</div>
            <h3>คำใบ้ปริศนา</h3>
            <p class="clue-text">"{target.clue_text}"</p>
            <div class="location">
                <strong>โซนจัดแสดง:</strong> {target.gallery_name} (ห้อง {target.room_no})
            </div>
        </div>

        <a href="/scan" class="action-btn">เจอแล้ว! ไปกรอกรหัสกันเลย</a>
    {:else}
        <div class="target-card">
            <div class="icon">⚠️</div>
            <h3>ยังไม่มีเป้าหมาย</h3>
            <p class="clue-text">กรุณาทำแบบทดสอบ (Quiz) เพื่อรับ Faction และเริ่มภารกิจ</p>
        </div>
        <a href="/quiz" class="action-btn">ไปทำ Quiz</a>
    {/if}
</div>

<style>
    .clue-container { text-align: center; }
    .target-card {
        background: #1a1a2e;
        border: 2px dashed #cda434;
        border-radius: 12px;
        padding: 40px 20px;
        margin: 20px auto;
        max-width: 400px;
    }
    .icon { font-size: 4rem; margin-bottom: 20px; }
    .clue-text { font-size: 1.2rem; font-style: italic; color: #ddd; line-height: 1.6; }
    .location { margin-top: 20px; color: #cda434; font-weight: bold; font-size: 1.1rem; }
    .action-btn {
        display: inline-block;
        background: #cda434;
        color: black;
        padding: 12px 24px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 8px;
        margin-top: 20px;
        transition: transform 0.2s;
    }
    .action-btn:hover {
        transform: scale(1.05);
    }
</style>