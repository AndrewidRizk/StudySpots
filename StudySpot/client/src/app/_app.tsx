import type { AppProps } from "next/app";
import Head from "next/head";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>{process.env.APP_NAME || "Default App Name"}</title>
        <meta
          name="description"
          content={process.env.APP_DESCRIPTION || "Default App Description"}
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
