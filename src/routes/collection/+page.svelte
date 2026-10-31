<script>
    let { data } = $props();
    let collections = $derived(data.collections || []);
    // @ts-ignore
    let collectedCount = $derived(collections.filter((item) => !item.is_locked).length);
</script>

<div class="collection-container">
    <h2>My Collection</h2>
    <p>All relics gathered in your journey ({collectedCount}/{collections.length} items)</p>
    
    {#if collections.length === 0}
        <div class="empty-state">
            <p>You don't have any artifacts in your collection yet.</p>
            <a href="/quiz" class="btn">Take Quiz to Claim Your First Relic!</a>
        </div>
    {:else}
        <div class="grid">
            {#each collections as item}
                <div class="card {item.is_locked ? 'locked' : 'unlocked'}">
                    <div class="card-image">
                        {#if item.is_locked}
                            <div class="question-mark">?</div>
                        {:else}
                            <img src={item.image_url || 'https://via.placeholder.com/150/1a1a2e/cda434?text=Artifact'} alt={item.name} />
                        {/if}
                    </div>

                    <div class="card-info">
                        <h3 class="title">{item.is_locked ? '???' : item.name}</h3>
                        
                        {#if item.is_locked}
                            <p class="room">Location: {item.gallery_name} (Room {item.room_no})</p>
                            <div class="status-badge locked-badge">LOCKED</div>
                        {:else}
                            <p class="faction">Zone: {item.gallery_name}</p>
                            <div class="status-badge unlocked-badge">UNLOCKED</div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .collection-container { text-align: center; }
    h2 { color: #cda434; }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    .empty-state {
        margin-top: 50px;
        padding: 40px;
        background: #1a1a2e;
        border: 1px dashed #cda434;
        border-radius: 12px;
    }
    .btn {
        display: inline-block;
        background: #cda434;
        color: black;
        padding: 10px 20px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 6px;
        margin-top: 15px;
    }

    /* Style ของ Card */
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
    }
    .card.locked { 
        border-color: #444; 
        opacity: 0.75; 
        background-color: #12121c;
    }
    
    .card-image {
        width: 100%;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #0f0f1a;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .card-image img { width: 100%; height: 100%; object-fit: cover; }
    
    .question-mark { font-size: 3.5rem; color: #555; font-weight: bold; }
    .title { color: #cda434; margin: 0 0 8px 0; font-size: 1.1rem; }
    .room { font-weight: bold; color: #aaa; font-size: 0.85rem; margin: 5px 0; }
    .faction { color: #ddd; font-size: 0.9rem; margin: 5px 0; }
    
    .status-badge {
        margin-top: 10px;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .unlocked-badge {
        background-color: #cda434;
        color: #000;
    }
    .locked-badge {
        background-color: #333;
        color: #888;
    }
</style>