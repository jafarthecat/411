<script>
	let { children } = $props();
</script>

<nav class="navbar">
	<a href="/" class="nav-link">Home</a>
	<a href="/quiz" class="nav-link">Quiz</a>
	<a href="/clue" class="nav-link">Clue</a>
	<a href="/unlock" class="nav-link">Unlock</a>
	<a href="/collection" class="nav-link">My Collection</a>
</nav>

	{@render children()}

<style>
    :global(html), :global(body) {
        margin: 0;
        padding: 0;
        background-color: #080808 !important;
        color: #f5f5f5;
        font-family: Arial, sans-serif;
        min-height: 100vh;
    }
</style>

