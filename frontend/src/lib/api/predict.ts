import { PUBLIC_API_BASE_URL } from '$env/static/public';

export type PredictionResult = {
	prediction: 'disaster' | 'not_disaster';
	probability: number;
	threshold: number;
};

export async function predictTweet(text: string): Promise<PredictionResult> {
	const response = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/predict`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			text
		})
	});

	if (!response.ok) {
		throw new Error(`Prediction failed: ${response.status}`);
	}

	return await response.json();
}
