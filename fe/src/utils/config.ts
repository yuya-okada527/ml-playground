const Config = () => {
  return {
    apiEndpoint: process.env.NEXT_PUBLIC_API_ENDPOINT,
  };
};

const config = Config();

export default config;
