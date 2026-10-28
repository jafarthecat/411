<script>
    let { item } = $props();
</script>

<div class="card {item.is_locked ? 'locked' : 'unlocked'}">
    <div class="card-image">
        {#if item.is_locked}
            <div class="question-mark">?</div>
        {:else}
            <!-- ถ้ามี image_url ให้แสดงรูป ถ้าไม่มีใช้รูปจำลอง -->
            <img src={item.image_url || 'https://via.placeholder.com/150/1a1a2e/cda434?text=Artifact'} alt={item.name} />
        {/if}
    </div>

    <div class="card-info">
        <h3 class="title">{item.is_locked ? '???' : item.name}</h3>
        
        {#if item.is_locked}
            <p class="clue">คำใบ้: {item.clue_text}</p>
            <p class="room">สถานที่: ห้อง {item.room_no}</p>
        {:else}
            <p class="faction">Faction ID: {item.faction_id}</p>
            <div class="badge">ปลดล็อกแล้ว</div>
        {/if}
    </div>
</div>

<style>
    .card {
        background-color: #1a1a2e;
        border: 2px solid #cda434;
        border-radius: 12px;
        padding: 15px;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: transform 0.2s;
    }
    .card:hover { transform: scale(1.02); }
    .card.locked { border-color: #555; opacity: 0.8; }
    
    .card-image {
        width: 100%;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #0f0f1a;
        border-radius: 8px;
        margin-bottom: 15px;
        overflow: hidden;
    }
    .card-image img { width: 100%; height: 100%; object-fit: cover; }
    
    .question-mark { font-size: 4rem; color: #555; font-weight: bold; }
    .title { color: #cda434; margin: 0 0 10px 0; font-size: 1.2rem; }
    .clue { font-style: italic; font-size: 0.9rem; color: #aaa; margin: 5px 0; }
    .room { font-weight: bold; color: #ddd; margin: 5px 0; }
    .badge {
        margin-top: 10px;
        background-color: #cda434;
        color: #000;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>