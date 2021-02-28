/* eslint-disable jsx-a11y/anchor-is-valid */
// TODO 暫定対応
import { Grid } from "@material-ui/core";
import Link from "next/link";
import Layout from "../components/Layout";

const AboutPage: React.FC = () => (
  <Layout title="About This Site">
    <Grid container>
      <Grid item xs={8}>
        <h1>このサイトについて</h1>
        <p>
          このサイトは、機械学習を活用したアプリケーションのデモンストレーション環境を提供します。
        </p>
        <p>
          収益化を主目標としていませんが、機械学習を活用したサービスを実環境で継続的に運用・改善していくためことを前提に設計・開発しています。
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
