<script>
    let { data, form } = $props();
    let step = $state('start');
    let currentIndex = $state(0);
    /** @type {string[]} */
    let answers = $state([]);

    function startQuiz() {
        answers = [];
        currentIndex = 0;
        step = 'quiz';
    }

    /** @param {string} choice */
    function choose(choice) {
        answers[currentIndex] = choice;
        if (currentIndex < data.questions.length - 1) currentIndex++;
        else step = 'review';
    }

    function back() {
        if (currentIndex > 0) currentIndex--;
        else step = 'start';
    }
</script>

<svelte:head>
    <title>Museum Persona Quiz | The British Museum</title>
    <meta name="description" content="Five unusual encounters. Choose NOPE or LIKE to find your museum persona." />
</svelte:head>

<main>
    <div class="brand">THE BRITISH MUSEUM <span>PERSONA QUIZ</span></div>
    {#if form?.success && step === 'start'}
        <section class="intro result">
            <p class="eyebrow">QUIZ COMPLETED</p>
            <p class="eyebrow">YOUR FACTION</p>
            <h1>{form.faction}</h1>
            <p class="dialogue">{factionDialogue[form.faction] || '“การเลือกของคุณได้กำหนดเส้นทางแล้ว นักสำรวจ—เบาะแสแรกกำลังรอคุณอยู่”'}</p>
            <p>การเดินทางเริ่มต้นแล้ว คุณได้รับวัตถุโบราณชิ้นแรก: <strong>{form.artifact}</strong></p>
            
            {#if form.imageUrl}
                <img src={form.imageUrl} alt={form.artifact} style="max-width: 100%; max-height: 250px; object-fit: contain; border-radius: 12px; margin: 20px 0;" />
            {/if}
            
            <p class="note">บันทึกวัตถุโบราณลงในคอลเลกชันแล้ว ไปดูคำใบ้ชิ้นต่อไปได้เลย</p>
        </section>
    {:else if step === 'start'}
        <section class="intro">
            <p class="eyebrow">FIND YOUR MUSEUM PERSONA</p>
            <h1>Ancient artifacts.<br />Modern problems.</h1>
            <p>Five unexpected encounters.<br />Would you say nope, or fall in love?</p>
            <div class="preview" aria-hidden="true">
                <img src="/images/quiz/hor.jpg" alt="" />
                <img src="/images/quiz/parthenon.jpg" alt="" />
                <img src="/images/quiz/serpent.jpg" alt="" />
            </div>
            <button class="gold" onclick={startQuiz}>BEGIN THE QUIZ →</button>
            <form method="POST" action="?/draw" style="width: 100%;">
    <button class="gold draw-fate" type="submit" style="cursor: pointer; width: 100%;">DRAW YOUR FATE</button>
</form>
            <p class="note">5 questions · No right or wrong answers</p>
        </section>
    {:else if step === 'quiz'}
        <div class="toolbar">
            <button class="back" onclick={back}>← BACK</button>
            <span aria-live="polite">{currentIndex + 1} / {data.questions.length}</span>
        </div>
        <progress value={currentIndex + 1} max={data.questions.length} aria-label="Question progress"></progress>
        {#each data.questions as question, index}
            {#if index === currentIndex}
                <article>
                    <h1>{index + 1}. {question.title}</h1>
                    <figure>
                        <img class="artifact" src={question.image} alt={question.artifact} />
                        <figcaption>{question.credit}</figcaption>
                    </figure>
                    <h2><strong>Artifact:</strong> {question.artifact}</h2>
                    <p class="question">{question.question}</p>
                    <div class="choices">
                        <button class="choice nope" class:selected={answers[index] === 'nope'} aria-pressed={answers[index] === 'nope'} onclick={() => choose('nope')}>
                            <span class="symbol" aria-hidden="true">×</span>
                            <span>NOPE</span>
                            <small>{question.nope}</small>
                        </button>
                        <button class="choice like" class:selected={answers[index] === 'like'} aria-pressed={answers[index] === 'like'} onclick={() => choose('like')}>
                            <span class="symbol" aria-hidden="true">♡</span>
                            <span>LIKE</span>
                            <small>{question.like}</small>
                        </button>
                    </div>
                    <a class="source" href={question.source} target="_blank" rel="noreferrer">Image source ↗</a>
                </article>
            {/if}
        {/each}
    {:else if step === 'review'}
        <section class="review">
            <p class="eyebrow">ALL FIVE ENCOUNTERS COMPLETE</p>
            <h1>Your choices</h1>
            <p>ตรวจคำตอบก่อนส่ง ย้อนกลับไปแก้ไขได้ทุกข้อ</p>
            <form method="POST" action="?/submit">
                {#each data.questions as question, index}
                    <input type="hidden" name="question_{question.id}" value={answers[index]} />
                    <div class="review-row">
                        <img src={question.image} alt="" />
                        <div><h2>{question.title}</h2><span class:liked={answers[index] === 'like'}>{answers[index] === 'like' ? '♡ LIKE' : '× NOPE'}</span></div>
                        <button type="button" class="back" onclick={() => { currentIndex = index; step = 'quiz'; }}>แก้ไข</button>
                    </div>
                {/each}
                <p class="note">“ทุกคำตอบคือร่องรอย ตรวจให้แน่ใจว่าคุณพร้อม แล้วเราจะเปิดเส้นทางให้”</p>
                <button class="gold" type="submit">ยืนยันคำตอบ →</button>
            </form>
        </section>
    {/if}
    {#if form?.error}<p class="error" role="alert">{form.error}</p>{/if}
    {#if data.offline}<p class="offline">กำลังใช้ชุดคำถามในโปรเจค — ยังไม่เชื่อม FastAPI</p>{/if}
</main>

<style>
    :global(body) { margin: 0; background: #080808; color: #f5f5f5; font-family: Arial, sans-serif; }
    main { max-width: 1080px; margin: 0 auto; padding: 30px 24px 48px; }
    .brand { display: flex; justify-content: space-between; gap: 16px; padding-bottom: 26px; border-bottom: 1px solid #2b2b2b; font-size: 12px; font-weight: bold; letter-spacing: 2px; }
    .brand span, .eyebrow { color: #ccad4c; }
    button { font: inherit; cursor: pointer; }
    button:focus-visible, a:focus-visible { outline: 3px solid #e4c968; outline-offset: 5px; }
    .intro { max-width: 620px; margin: 65px auto 35px; text-align: center; }
    .eyebrow { font-size: 11px; letter-spacing: 2px; }
    .intro h1 { font-family: Georgia, serif; font-size: clamp(36px, 6vw, 64px); line-height: 1.1; margin: 24px 0; }
    p { color: #b9b9b9; line-height: 1.6; }
    .preview { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 30px 0; }
    .preview img { width: 100%; height: 160px; object-fit: cover; border-radius: 12px; }
    .gold { background: #ccad4c; color: #14120b; padding: 16px 24px; border: 0; border-radius: 6px; font-weight: bold; width: 100%; }
    .gold:hover { background: #e4c968; }
    .draw-fate { margin-top: 12px; cursor: default; }
    .note, .offline { font-size: 12px; color: #999; }
    .offline { text-align: center; margin-top: 35px; }
    .toolbar { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; color: #ccad4c; font-size: 13px; }
    .back:hover { color: #e4c968; }
    progress { display: block; width: 100%; height: 5px; margin: 12px 0 26px; accent-color: #ccad4c; border: 0; border-radius: 4px; background: #333; }
    progress::-webkit-progress-bar { background: #333; border-radius: 4px; }
    progress::-webkit-progress-value { background: #ccad4c; border-radius: 4px; }
    article h1 { font-size: clamp(22px, 3vw, 30px); margin: 0 0 20px; line-height: 1.3; }
    figure { margin: 0; position: relative; }
    .artifact { display: block; width: 100%; height: clamp(230px, 42vw, 500px); object-fit: contain; background: #202020; border-radius: 22px; }
    figcaption { position: absolute; bottom: 12px; left: 12px; max-width: 80%; padding: 7px 12px; border-radius: 20px; background: #000a; color: #eee; font-size: 11px; }
    h2 { font-size: 22px; font-weight: normal; line-height: 1.4; margin: 16px 0 10px; }
    .question { font-size: 19px; margin: 12px 0 18px; min-height: 60px; }
    .choices { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .choice { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; background: #242424; color: #fff; border: 2px solid transparent; border-radius: 18px; padding: 15px; min-height: 125px; font-size: 20px; }
    .choice small { font-size: 16px; line-height: 1.4; }
    .symbol { font-size: 30px; line-height: 1; }
    .nope .symbol { color: #e55252; }
    .like .symbol, .liked { color: #59bb79; }
    .nope:hover, .nope.selected { border-color: #e55252; background: #302121; }
    .like:hover, .like.selected { border-color: #59bb79; background: #203026; }
    .source { display: block; text-align: right; margin-top: 18px; color: #b6b6b6; font-size: 12px; }
    .review { max-width: 720px; margin: 45px auto; }
    .review-row { display: flex; gap: 18px; align-items: center; padding: 18px 0; border-bottom: 1px solid #303030; }
    .review-row img { width: 70px; height: 70px; object-fit: cover; border-radius: 8px; }
    .review-row div { flex: 1; }
    .review-row h2 { font-size: 16px; margin: 0 0 8px; }
    .review-row span { font-size: 12px; }
    .error { color: #f08b8b; text-align: center; }
    @media (max-width: 600px) {
        main { padding: 24px 16px; }
        .brand { font-size: 9px; letter-spacing: 1px; }
        .intro { margin-top: 45px; }
        .preview img { height: 110px; }
        .question { font-size: 16px; }
        h2 { font-size: 18px; }
        .choice { font-size: 17px; min-height: 120px; padding: 12px 8px; }
        .choice small { font-size: 13px; }
        .review-row { gap: 10px; }
        figcaption { font-size: 9px; }
    }
</style>
