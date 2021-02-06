type QueriesType = {
  [key: string]: string | boolean | number | string[] | boolean[] | number[];
};

const callGetApi = async (url: string, queries: QueriesType) => {
  // クエリ文字列を作成
  const queryStr = makeQuery(queries);

  // URLを組み立て
  const requestUrl = url + "?" + queryStr;

  // リクエスト
  return await fetch(requestUrl, {
    method: "GET",
  })
    .then(async (response) => {
      console.log(response);
      return await response.json();
    })
    .catch((err) => {
      // TODO ログ
      console.log(err);
      return;
    });
};

const makeQuery = (queries: QueriesType): string => {
  let result = [];
  for (let entry of Object.entries(queries)) {
    let key = entry[0];
    if (Array.isArray(entry[1])) {
      for (let value of entry[1]) {
        result.push(key + "=" + value);
      }
    } else {
      result.push(key + "=" + entry[1]);
    }
  }

  return result.join("&");
};

export { callGetApi };
