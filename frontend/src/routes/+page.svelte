<script lang="ts">
	import { predictTweet, type PredictionResult } from '$lib/api/predict';

	let text = $state('');
	let result = $state<PredictionResult | null>(null);

	let isLoading = $state(false);
	let errorMessage = $state('');

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		const trimmedText = text.trim();

		if (!trimmedText) {
			errorMessage = 'ツイートを入力してください.';

			result = null;

			return;
		}

		isLoading = true;
		errorMessage = '';
		result = null;

		try {
			result = await predictTweet(trimmedText);
		} catch (error) {
			console.error(error);

			errorMessage = '判定中にエラーが発生しました。';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Disaster Tweet Classifier</title>

	<meta
		name="description"
		content="DistilBERTを使って、入力されたツイートが災害に関するものか判定します。"
	/>
</svelte:head>

<main>
	<section>
		<h1>Disaster Tweet Classifier</h1>

		<p>入力したツイートが実際の災害について 書かれているかAIが判定します。</p>

		<form onsubmit={handleSubmit}>
			<label for="tweet"> ツイート </label>

			<textarea
				id="tweet"
				bind:value={text}
				rows="6"
				maxlength="1000"
				placeholder="Enter a tweet..."
				disabled={isLoading}></textarea>

			<p>
				{text.length} / 1000
			</p>

			<button type="submit" disabled={isLoading || text.trim().length === 0}>
				{isLoading ? '判定中...' : '判定する'}
			</button>
		</form>

		{#if errorMessage}
			<p role="alert">
				{errorMessage}
			</p>
		{/if}

		{#if result}
			<section>
				<h2>判定結果</h2>

				{#if result.prediction === 'disaster'}
					<p>災害ツイート</p>
				{:else}
					<p>非災害ツイート</p>
				{/if}

				<p>
					災害確率：
					{(result.probability * 100).toFixed(1)}%
				</p>

				<p>
					判定閾値：
					{(result.threshold * 100).toFixed(0)}%
				</p>
			</section>
		{/if}
	</section>
</main>
