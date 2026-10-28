<script>
    import { goto } from '$app/navigation';

    // สถานะหน้า: 'start' (หน้าแรก), 'quiz' (กำลังทำ), 'result' (ผลลัพธ์)
    let step = $state('start'); 
    let currentIndex = $state(0);
    // @ts-ignore
    let answers = $state([]);
    let loading = $state(false);
    let errorMessage = $state('');

    const questions = [
        {
            id: 1,
            title: "เมื่อพบประตูโบราณที่ปิดล๊อคอยู่...",
            leftText: "วิเคราะห์อักขระและถอดรหัสกลไก",
            leftFaction: "Egypt",
            rightText: "ใช้กำลังและอาวุธพังประตูเข้าไป",
            rightFaction: "Rome"
        },
        {
            id: 2,
            title: "สิ่งของคู่กายที่คุณไว้วางใจมากที่สุด...",
            leftText: "ตำราพิชัยสงครามและแผนที่",
            leftFaction: "Greece",
            rightText: "เครื่องรางโบราณและเวทมนตร์",
            rightFaction: "Egypt"
        },
        {
            id: 3,
            title: "เป้าหมายสูงสุดของการสำรวจครั้งนี้...",
            leftText: "บันทึกประวัติศาสตร์และปรัชญา",
            leftFaction: "Greece",
            rightText: "ครอบครองสมบัติและแผ่ขยายอำนาจ",
            rightFaction: "Rome"
        },
        {
            id: 4,
            title: "บรรยากาศสถานที่ที่คุณชอบมากที่สุด...",
            leftText: "วิหารหินอ่อนบนยอดเขาอันสงบ",
            leftFaction: "Greece",
            rightText: "พีระมิดและโบราณสถานกลางทะเลทราย",
            rightFaction: "Egypt"
        }
    ];

    function startQuiz() {
        step = 'quiz';
        currentIndex = 0;
        answers = [];
    }

    // @ts-ignore
    function selectOption(faction) {
        answers.push(faction);
        if (currentIndex < questions.length - 1) {
            currentIndex++;
        } else {
            submitAnswers(answers);
        }
    }

    function randomQuiz() {
        const factions = ['Egypt', 'Greece', 'Rome'];
        const randomAnswers = [
            factions[Math.floor(Math.random() * factions.length)],
            factions[Math.floor(Math.random() * factions.length)],
            factions[Math.floor(Math.random() * factions.length)],
            factions[Math.floor(Math.random() * factions.length)]
        ];
        submitAnswers(randomAnswers);
    }

    // @ts-ignore
    async function submitAnswers(finalAnswers) {
        loading = true;
        errorMessage = '';
        step = 'result';

        try {
            const res = await fetch('http://127.0.0.1:8000/personas/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 1,
                    scenario_1_choice: finalAnswers[0],
                    scenario_2_choice: finalAnswers[1],
                    scenario_3_choice: finalAnswers[2],
                    scenario_4_choice: finalAnswers[3]
                })
            });

            const data = await res.json();

            if (!res.ok) {
                // ถ้า Backend แจ้งว่าทำควิซไปแล้ว
                if (data.detail && data.detail.includes("ทำแบบทดสอบ")) {
                    throw new Error("คุณเคยทำ Quiz เพื่อรับ Faction และ Artifact ชิ้นแรกไปเรียบร้อยแล้ว!");
                }
                throw new Error(data.detail || 'เกิดข้อผิดพลาดในการทำ Quiz');
            }

            // ทำสำเร็จ ย้ายไปหน้า Collection
            goto('/collection');
        } catch (err) {
            // @ts-ignore
            errorMessage = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="quiz-wrapper">
    {#if step === 'start'}
        <!-- หน้าเริ่มต้นทำ Quiz -->
        <div class="start-card">
            <div class="icon">🏛️</div>
            <h2>ค้นหา Faction ประจำตัวคุณ</h2>
            <p>ตอบคำถามปริศนา 4 ข้อ เพื่อปลดล็อก Faction และรับ Artifact ชิ้นแรกเข้าสู่คอลเลกชันของคุณ!</p>
            
            <div class="start-buttons">
                <button class="btn-primary" onclick={startQuiz}>
                    ✨ เริ่มทำ Quiz
                </button>
                <button class="btn-random" onclick={randomQuiz}>
                    🎲 สุ่มการ์ดทันที
                </button>
            </div>
        </div>

    {:else if step === 'quiz'}
        <!-- หน้าทำการ์ดปัด ซ้าย-ขวา -->
        <div class="quiz-card-container">
            <div class="progress">ข้อ {currentIndex + 1} / {questions.length}</div>
            
            <div class="swipe-card">
                <h3>{questions[currentIndex].title}</h3>
                <div class="swipe-actions">
                    <button class="btn-swipe left" onclick={() => selectOption(questions[currentIndex].leftFaction)}>
                        <span class="arrow">⬅️</span>
                        <span>{questions[currentIndex].leftText}</span>
                    </button>
                    
                    <div class="divider">VS</div>

                    <button class="btn-swipe right" onclick={() => selectOption(questions[currentIndex].rightFaction)}>
                        <span>{questions[currentIndex].rightText}</span>
                        <span class="arrow">➡️</span>
                    </button>
                </div>
            </div>
        </div>

    {:else if step === 'result'}
        <!-- หน้ากำลังประมวลผล / แสดง Error -->
        <div class="result-card">
            {#if loading}
                <div class="spinner">🔮</div>
                <h3>กำลังวิเคราะห์ผลการค้นหา...</h3>
                <p>ระบบกำลังจัดสรร Faction และ Artifact ชิ้นแรกให้คุณ</p>
            {:else if errorMessage}
                <div class="info-box">
                    <div class="icon-small">🛡️</div>
                    <h3>รับการ์ดเรียบร้อยแล้ว</h3>
                    <p>{errorMessage}</p>
                    
                    <div class="action-buttons">
                        <a href="/clue" class="btn-gold">🔍 ไปดูคำใบ้ชิ้นถัดไป (Clue)</a>
                        <a href="/collection" class="btn-secondary">🖼️ ดูคอลเลกชันของคุณ</a>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .quiz-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;
        text-align: center;
    }

    .start-card, .swipe-card, .result-card {
        background: #1a1a2e;
        border: 2px solid #cda434;
        border-radius: 16px;
        padding: 40px 30px;
        max-width: 450px;
        width: 100%;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }

    .icon { font-size: 4rem; margin-bottom: 15px; }
    .icon-small { font-size: 3rem; margin-bottom: 10px; }
    h2 { color: #cda434; margin-bottom: 10px; }
    p { color: #ccc; line-height: 1.5; font-size: 0.95rem; }

    .start-buttons {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 30px;
    }

    .btn-primary {
        background: #cda434;
        color: #000;
        border: none;
        padding: 14px;
        font-size: 1.05rem;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .btn-primary:hover { transform: scale(1.02); }

    .btn-random {
        background: #2a2a40;
        color: #fff;
        border: 1px solid #cda434;
        padding: 12px;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .btn-random:hover { background: #353554; }

    .progress {
        color: #cda434;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .swipe-card h3 {
        color: #fff;
        font-size: 1.2rem;
        margin-bottom: 30px;
        min-height: 50px;
    }
    .swipe-actions {
        display: flex;
        flex-direction: column;
        gap: 15px;
        align-items: center;
    }

    .btn-swipe {
        background: #0f0f1a;
        border: 1px solid #444;
        color: #ddd;
        padding: 15px;
        border-radius: 10px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.95rem;
    }
    .btn-swipe:hover {
        border-color: #cda434;
        color: #cda434;
        background: #252538;
    }

    .divider { color: #666; font-weight: bold; font-size: 0.8rem; }

    .spinner { font-size: 3.5rem; animation: spin 2s infinite linear; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    .info-box h3 { color: #cda434; font-size: 1.3rem; margin-bottom: 10px; }
    .action-buttons {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
    }

    .btn-gold {
        background: #cda434;
        color: #000;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
    }
    .btn-secondary {
        background: #222;
        color: #aaa;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        border: 1px solid #444;
    }
</style>