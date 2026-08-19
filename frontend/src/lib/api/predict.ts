import { PUBLIC_API_BASE_URL } from '$env/static/public';

export type PredictionResult = {
	prediction: 'disaster' | 'not_disaster';
	probability: number;
	threshold: number;
};

export class PredictionApiError extends Error {
	status: number;

	constructor(message: string, status: number) {
		super(message);

		this.name = 'PredictionApiError';
		this.status = status;
	}
}

export async function predictTweet(text: string, signal?: AbortSignal): Promise<PredictionResult> {
	const response = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/predict`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			text
		}),
		signal
	});

	if (!response.ok) {
		throw new PredictionApiError('Prediction request failed.', response.status);
	}

	const data: unknown = await response.json();

	if (
		typeof data !== 'object' ||
		data === null ||
		!('prediction' in data) ||
		!('probability' in data) ||
		!('threshold' in data)
	) {
		throw new Error('Invalid API response.');
	}

	return data as PredictionResult;
}
