<script lang="ts">
	import { predictTweet, PredictionApiError, type PredictionResult } from '$lib/api/predict';

	let text = $state('');
	let result = $state<PredictionResult | null>(null);
	let isLoading = $state(false);
	let errorMessage = $state('');

	const REQUEST_TIMEOUT_MS = 30_000;

	const disasterExample = 'Forest fire near La Ronge Sask. Canada';

	const nonDisasterExample = 'I had a great lunch with my friends today!';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (isLoading) {
			return;
		}

		const trimmedText = text.trim();

		if (!trimmedText) {
			errorMessage = 'ツイートを入力してください。';

			result = null;

			return;
		}

		isLoading = true;
		errorMessage = '';
		result = null;

		const controller = new AbortController();

		const timeoutId = window.setTimeout(() => {
			controller.abort();
		}, REQUEST_TIMEOUT_MS);

		try {
			result = await predictTweet(trimmedText, controller.signal);
		} catch (error) {
			console.error(error);

			if (error instanceof DOMException && error.name === 'AbortError') {
				errorMessage = '判定に時間がかかっています。しばらくしてからもう一度お試しください。';
			} else if (error instanceof PredictionApiError) {
				if (error.status === 422) {
					errorMessage = '入力内容を確認してください。';
				} else if (error.status >= 500) {
					errorMessage = 'サーバーでエラーが発生しました。';
				} else {
					errorMessage = '判定リクエストに失敗しました。';
				}
			} else {
				errorMessage = 'サーバーに接続できませんでした。';
			}
		} finally {
			window.clearTimeout(timeoutId);

			isLoading = false;
		}
	}

	function handleInput() {
		result = null;
		errorMessage = '';
	}

	function setExample(example: string) {
		text = example;
		result = null;
		errorMessage = '';
	}
</script>

<svelte:head>
	<title>Disaster Tweet Classifier</title>

	<meta
		name="description"
		content="DistilBERTを使って、入力されたツイートが災害に関するものか判定します。"
	/>
</svelte:head>

<main class="min-h-screen bg-slate-50 px-4 py-12 sm:px-6">
	<div class="mx-auto w-full max-w-2xl">
		<header class="mb-8 text-center">
			<p class="mb-2 text-sm font-semibold tracking-widest text-slate-500 uppercase">
				DistilBERT 5-Fold Ensemble
			</p>

			<h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
				Disaster Tweet Classifier
			</h1>

			<p class="mx-auto mt-4 max-w-xl text-sm leading-6 text-slate-600 sm:text-base">
				英語のツイートを入力すると、 AIが実際の災害に関する投稿かどうかを判定します。
			</p>
		</header>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
			<form onsubmit={handleSubmit} class="space-y-5">
				<div>
					<label for="tweet" class="mb-2 block text-sm font-semibold text-slate-800"> Tweet </label>

					<textarea
						id="tweet"
						bind:value={text}
						oninput={handleInput}
						rows="7"
						maxlength="1000"
						placeholder="Enter an English tweet..."
						disabled={isLoading}
						class="w-full resize-none rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm leading-6 text-slate-900 transition outline-none placeholder:text-slate-400 focus:border-slate-500 focus:ring-2 focus:ring-slate-200 disabled:cursor-not-allowed disabled:bg-slate-100"
					></textarea>

					<div class="mt-2 flex items-center justify-between gap-4">
						<p class="text-xs text-slate-500">英語のツイートを入力してください</p>

						<p class="text-xs text-slate-500 tabular-nums">
							{text.length} / 1000
						</p>
					</div>
				</div>

				<div class="flex flex-wrap gap-2">
					<button
						type="button"
						onclick={() => setExample(disasterExample)}
						disabled={isLoading}
						class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-700 transition hover:bg-slate-100 disabled:opacity-50"
					>
						災害例を入力
					</button>

					<button
						type="button"
						onclick={() => setExample(nonDisasterExample)}
						disabled={isLoading}
						class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-700 transition hover:bg-slate-100 disabled:opacity-50"
					>
						非災害例を入力
					</button>
				</div>

				<button
					type="submit"
					disabled={isLoading || text.trim().length === 0}
					class="flex w-full items-center justify-center rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-300"
				>
					{#if isLoading}
						<span
							class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
						></span>

						判定中...
					{:else}
						判定する
					{/if}
				</button>
			</form>

			{#if errorMessage}
				<div
					role="alert"
					class="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
				>
					{errorMessage}
				</div>
			{/if}
		</section>

		{#if result}
			<section
				aria-live="polite"
				class="mt-6 rounded-2xl border bg-white p-6 shadow-sm sm:p-8"
				class:border-red-200={result.prediction === 'disaster'}
				class:border-emerald-200={result.prediction === 'not_disaster'}
			>
				<p class="text-sm font-medium text-slate-500">判定結果</p>

				<div class="mt-2 flex items-center gap-3">
					{#if result.prediction === 'disaster'}
						<div class="flex h-10 w-10 items-center justify-center rounded-full bg-red-100 text-xl">
							⚠️
						</div>

						<div>
							<h2 class="text-2xl font-bold text-red-700">災害ツイート</h2>

							<p class="text-sm text-slate-500">Disaster</p>
						</div>
					{:else}
						<div
							class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 text-xl"
						>
							✓
						</div>

						<div>
							<h2 class="text-2xl font-bold text-emerald-700">非災害ツイート</h2>

							<p class="text-sm text-slate-500">Not disaster</p>
						</div>
					{/if}
				</div>

				<div class="mt-6">
					<div class="mb-2 flex items-end justify-between">
						<span class="text-sm font-medium text-slate-700"> 災害確率 </span>

						<span class="text-2xl font-bold text-slate-900 tabular-nums">
							{(result.probability * 100).toFixed(1)}%
						</span>
					</div>

					<div class="h-3 overflow-hidden rounded-full bg-slate-100">
						<div
							class="h-full rounded-full bg-slate-700 transition-all duration-500"
							style:width={`${result.probability * 100}%`}
						></div>
					</div>

					<div class="mt-2 flex justify-between text-xs text-slate-500">
						<span> 0% </span>

						<span>
							判定閾値
							{(result.threshold * 100).toFixed(0)}%
						</span>

						<span> 100% </span>
					</div>
				</div>
			</section>
		{/if}

		<section class="mt-8 rounded-2xl border border-slate-200 bg-white p-5 text-sm text-slate-600">
			<h2 class="font-semibold text-slate-900">モデルについて</h2>

			<p class="mt-2 leading-6">
				Kaggle「Natural Language Processing with Disaster Tweets」で学習した DistilBERTの5-Fold
				Ensembleを使用しています。 5モデルの災害確率を平均し、 0.49を判定閾値として分類します。
			</p>
		</section>
	</div>
</main>
