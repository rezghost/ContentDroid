import applicationConfig from "../configurations/app-config";
import ApplicationConfig from "../types/application-config";
    
export class GenerationService {
    private config : ApplicationConfig = applicationConfig;

    async generateVideoAsync(prompt: string): Promise<string> {
        const response = await fetch(`${this.config.generationServiceUrl}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });

        if (!response.ok) {
            throw new Error(`Generation failed: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    }
}