import { useRouter } from "next/router";

const DetailPage = () => {
  const router = useRouter();
  const { movie_id } = router.query;

  return <p>movie_id: {movie_id}</p>;
};

export default DetailPage;
