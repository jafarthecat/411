<script>
	let { form } = $props();
</script>

<div class="scan-container">
	<h2>Scan or Insert Code</h2>
	<p>กรอกรหัสที่พบป้ายข้าง Artifact เพื่อปลดล็อกเข้าสู่คอลเลกชัน</p>

	<!-- พื้นที่จำลองกล้องสแกน (เผื่อต่อยอดใช้ html5-qrcode) -->
	<div class="scanner-placeholder">
		<p>[ กล้องสแกน QR Code ]</p>
	</div>

	<h3>OR</h3>

	{#if form?.message}
		<div class="alert {form.success ? 'success' : 'error'}">
			{form.message}
		</div>
	{/if}

	<form method="POST" action="?/submitCode" class="code-form">
		<input type="text" name="artifact_code" placeholder="กรอกรหัส Artifact ที่นี่ (เช่น ROSETTA01)" required />
		<button type="submit">ปลดล็อก</button>
	</form>
</div>

<style>
	.scan-container { text-align: center; max-width: 500px; margin: 0 auto; }
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
		padding: 12px;
		border-radius: 8px;
		border: 1px solid #cda434;
		background: #1a1a2e;
		color: white;
	}
	button {
		padding: 12px 24px;
		background: #cda434;
		color: black;
		border: none;
		border-radius: 8px;
		font-weight: bold;
		cursor: pointer;
	}
	.alert { padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; }
	.success { background: #d4edda; color: #155724; }
	.error { background: #f8d7da; color: #721c24; }
</style>