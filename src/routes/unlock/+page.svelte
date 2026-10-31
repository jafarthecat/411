<script>
    let { form } = $props();
</script>

<div class="scan-container">
    <h2>Scan or Enter Code</h2>
    <p>Enter the code found on the artifact display label to unlock.</p>

    {#if form?.message}
        <div class="alert {form.success ? 'success' : 'error'}">
            {form.message}
        </div>
    {/if}

    <form method="POST" action="?/submitCode" class="code-form">
        <input 
            type="text" 
            name="artifact_code" 
            placeholder="Enter Artifact Code" 
            required 
        />
        <button type="submit">Unlock</button>
    </form>
</div>

<style>
    .scan-container { text-align: center; max-width: 500px; margin: 40px auto; }
    .scanner-placeholder {
        background: #2a2a4e;
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #cda434;
        border-radius: 12px;
        margin: 20px 0;
        color: #888;
    }
    .code-form { display: flex; gap: 10px; margin-top: 20px; }
    input {
        flex-grow: 1;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #cda434;
        background: #1a1a2e;
        color: white;
        font-size: 15px;
    }
    input::placeholder { color: #888; }
    button {
        padding: 12px 24px;
        background: #cda434;
        color: black;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.2s;
    }
    button:hover {
        background: #e4c968;
    }
    .alert { padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; }
    .success { background: #1e3a29; color: #59bb79; border: 1px solid #59bb79; }
    .error { background: #3a1e1e; color: #e55252; border: 1px solid #e55252; }
</style>