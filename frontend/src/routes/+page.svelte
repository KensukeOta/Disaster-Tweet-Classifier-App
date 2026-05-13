<script lang="ts">
	import type { PredictResponse } from "$lib/api/predict";
	import { predictDisaster } from "$lib/api/predict";

	let text = $state("");
	let result = $state<PredictResponse | null>(null);
	let isLoading = $state(false);
	let errorMessage = $state("");

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!text.trim()) {
			errorMessage = "判定したい文章を入力してください。";
			return;
		}

		isLoading = true;
		errorMessage = "";
		result = null;

		try {
			result = await predictDisaster(text);
		} catch {
			errorMessage = "判定中にエラーが発生しました。";
		} finally {
			isLoading = false;
		}
	}

	const labelText = $derived(result?.label === "disaster" ? "災害関連" : "非災害関連");

	const probabilityPercent = $derived(result ? Math.round(result.probability * 100) : 0);
</script>

<svelte:head>
	<title>Disaster Tweet Classifier</title>
	<meta name="description" content="SNS投稿が災害関連かどうかをAIモデルで分類するアプリです。" />
</svelte:head>

<main class="mx-auto flex min-h-screen max-w-3xl flex-col px-6 py-12">
	<section class="mb-10">
		<p class="mb-3 text-sm font-semibold text-blue-600">AI Model Portfolio</p>
		<h1 class="mb-4 text-3xl font-bold tracking-tight text-gray-900">Disaster Tweet Classifier</h1>
		<p class="text-gray-600">
			SNS投稿文を入力すると、AIモデルが「災害関連」か「非災害関連」かを判定します。
		</p>
	</section>

	<form onsubmit={handleSubmit} class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
		<label for="tweet-text" class="mb-2 block font-semibold text-gray-900"> 投稿文 </label>

		<textarea
			id="tweet-text"
			bind:value={text}
			rows="6"
			placeholder="例: There is a fire near the station"
			class="w-full rounded-xl border border-gray-300 p-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
		></textarea>

		{#if errorMessage}
			<p class="mt-3 text-sm text-red-600">{errorMessage}</p>
		{/if}

		<button
			type="submit"
			disabled={isLoading}
			class="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
		>
			{isLoading ? "判定中..." : "判定する"}
		</button>
	</form>

	{#if result}
		<section class="mt-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-bold text-gray-900">判定結果</h2>

			<div class="space-y-3">
				<p>
					<span class="font-semibold">分類:</span>
					{labelText}
				</p>

				<p>
					<span class="font-semibold">災害関連である確率:</span>
					{probabilityPercent}%
				</p>

				<p>
					<span class="font-semibold">使用した閾値:</span>
					{result.threshold}
				</p>
			</div>
		</section>
	{/if}
</main>
