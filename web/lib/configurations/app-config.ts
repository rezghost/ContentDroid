import ApplicationConfig from "../types/application-config";

const applicationConfig : ApplicationConfig = {
  generationServiceUrl: process.env.GENERATION_SERVICE_URL || "http://localhost:8080",
};

export default applicationConfig;
