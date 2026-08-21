<script lang="ts">
	import './layout.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="/favicon.png" />

	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="Disaster Tweet-Classifier Appr" />
	<meta property="og:title" content="Disaster Tweet Classifier-Appr" />
	<meta
		property="og:description"
		content="英語のツイートが実際の災害に関する投稿かどうかを判定するWebアプリケーションです。"
	/>
	<meta
		property="og:image"
		content="https://disaster-tweet-classifier-app.vercel.app/ogp-image.png"
	/>

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Disaster Tweet Classifier App" />
	<meta
		name="twitter:description"
		content="英語のツイートが実際の災害に関する投稿かどうかを判定するWebアプリケーションです。"
	/>
	<meta
		name="twitter:image"
		content="https://disaster-tweet-classifier-app.vercel.app/ogp-image.png"
	/>
</svelte:head>

{@render children()}
