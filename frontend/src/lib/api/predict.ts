import { PUBLIC_API_BASE_URL } from "$env/static/public";

export type PredictResponse = {
	label: "disaster" | "not_disaster";
	prediction: number;
	probability: number;
	threshold: number;
};

export async function predictDisaster(text: string): Promise<PredictResponse> {
	const response = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/predict`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ text })
	});

	if (!response.ok) {
		throw new Error("予測に失敗しました");
	}

	return response.json();
}
