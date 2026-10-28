<script>
	let { children } = $props();
</script>

<nav class="navbar">
	<a href="/" class="nav-link">Home</a>
	<a href="/quiz" class="nav-link">Quiz</a>
	<a href="/clue" class="nav-link">Clue</a>
	<a href="/scan" class="nav-link">Scan / Code</a>
	<a href="/collection" class="nav-link">My Collection</a>
</nav>

	{@render children()}

