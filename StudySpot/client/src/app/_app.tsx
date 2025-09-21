import type { AppProps } from "next/app";
import Head from "next/head";
import { useEffect } from "react";
import * as FullStory from "@fullstory/browser";

function MyApp({ Component, pageProps }: AppProps) {
  useEffect(() => {
    // Only init FullStory in production
    if (process.env.NEXT_PUBLIC_FS_ORG_ID) {
      FullStory.init({ orgId: process.env.NEXT_PUBLIC_FS_ORG_ID });
    }
  }, []);

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_APP_NAME || "Default App Name"}</title>
        <meta
          name="description"
          content={
            process.env.NEXT_PUBLIC_APP_DESCRIPTION || "Default App Description"
          }
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
