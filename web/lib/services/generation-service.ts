export class GenerationService {
    async generateVideoAsync(prompt: string): Promise<string> {
        const response = await fetch(`/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });

        if (!response.ok) {
            throw new Error(`Generation failed: ${response.statusText}`);
        }

        const data = await response.text();
        return data;
    }

    async getDownloadStatusAsync(id: string): Promise<string> {
        const response = await fetch(`/api/status/${encodeURIComponent(id)}`, {});

        if (!response.ok) {
            throw new Error(`Status fetch failed: ${response.statusText}`);
        }

        const data = await response.text();
        return data;
    }

    async getVideoUriAsync(id: string): Promise<string> {
        const response = await fetch(`/api/video/${encodeURIComponent(id)}`, {});

        if (!response.ok) {
            throw new Error(`Video URI fetch failed: ${response.statusText}`);
        }

        const data = await response.text();
        return data;
    }
}
