import { createStyles, makeStyles, Theme } from "@material-ui/core";
import { Pagination } from "@material-ui/lab";
import React from "react";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    paginationRoot: {
      textAlign: "center",
      "& > * + *": {
        marginTop: theme.spacing(2),
      },
    },
    pagination: {
      display: "inline-block",
    },
  })
);

type SearchResultPaginationProps = {
  totalPageCount: number;
  currentPage: number;
  handlePageChange: (event: React.ChangeEvent<unknown>, page: number) => void;
};

/**
 * 検索結果のページネーションを描画する
 * @param totalPageCount 総ページ数
 * @param currentPage 現在のページ番号
 * @param handlePageChange ページ変更ハンドラ
 */
const SearchResultPagination: React.FC<SearchResultPaginationProps> = ({
  totalPageCount,
  currentPage,
  handlePageChange,
}) => {
  const classes = useStyles();
  return (
    <div className={classes.paginationRoot}>
      <Pagination
        count={totalPageCount}
        page={currentPage}
        color="primary"
        className={classes.pagination}
        onChange={handlePageChange}
      />
    </div>
  );
};

export default SearchResultPagination;
