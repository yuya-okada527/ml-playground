import { Grid } from "@material-ui/core";
import Link from "next/link";
import Layout from "../components/Layout";

const AboutPage = () => (
  <Layout title="About | Next.js + TypeScript Example">
    <Grid container>
      <Grid item xs={8}>
        <h1>このサイトについて</h1>
        <p>
          このサイトは、機械学習を活用したアプリケーションのデモンストレーション環境を提供します。
        </p>
        <p>
          収益化を主目標としていませんが、機械学習を活用したサービスを実環境で継続的に運用・改善していくための工夫を凝らし、設計・開発しています。
        </p>
        <p>現在、提供している機能は以下です。</p>
        <p>
          <Link href="/">
            <a>映画推薦</a>
          </Link>
        </p>
      </Grid>
    </Grid>
  </Layout>
);

export default AboutPage;
