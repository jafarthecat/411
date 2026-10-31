<script>
    let { data } = $props();
</script>

<main>
    <!-- 1. Check if user hasn't completed the quiz / drawn fate -->
    {#if !data.target || !data.target.has_quiz}
        <div class="locked-box" style="text-align: center; padding: 50px 20px;">
            <div style="font-size: 48px; margin-bottom: 12px;">🔒</div>
            <h2>Clue Locked</h2>
            <p style="color: #aaa; margin-bottom: 20px;">
                {data.target?.message || 'Please take the Quiz or Draw Your Fate first to reveal your first clue.'}
            </p>
            <a href="/quiz" class="gold-btn" style="display: inline-block; background: #ccad4c; color: #14120b; padding: 12px 24px; border-radius: 6px; font-weight: bold; text-decoration: none;">
                Take Quiz to Claim Starter Artifact →
            </a>
        </div>

    <!-- 2. Check if all 16 items have been collected -->
    {:else if data.target.completed}
        <div class="completed-box" style="text-align: center; padding: 50px 20px;">
            <div style="font-size: 48px; margin-bottom: 12px;">🏆</div>
            <h2>Collection Completed!</h2>
            <p style="color: #aaa;">Thank you for exploring all the treasures in the museum.</p>
        </div>

    <!-- 3. Show current target clue for active players -->
    {:else}
        <div class="clue-container">
            <p class="eyebrow" style="color: #ccad4c; font-size: 12px; letter-spacing: 2px;">CURRENT TARGET</p>
            
            <div class="card" style="border: 2px dashed #ccad4c; padding: 30px; border-radius: 12px; text-align: center; margin: 20px 0;">
                <div class="question-mark" style="font-size: 36px; color: #ff4d4d; font-weight: bold;">?</div>
                <p style="color: #ccc; margin-top: 10px;">Mystery Clue</p>
                <h2 style="font-size: 20px; font-style: italic; margin: 15px 0;">"{data.target.clue_text}"</h2>
                <p style="color: #ccad4c;">
                    Gallery: {data.target.gallery_name} (Room {data.target.room_no})
                </p>
            </div>

            <a href="/unlock" class="gold-btn" style="display: block; width: 100%; text-align: center; background: #ccad4c; color: #14120b; padding: 14px; border-radius: 6px; font-weight: bold; text-decoration: none;">
                Found It! Enter Code to Unlock →
            </a>
        </div>
    {/if}
</main>