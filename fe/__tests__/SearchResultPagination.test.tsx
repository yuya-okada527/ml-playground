import React from "react";
import { shallow } from "enzyme";
import SearchResultPagination from "../src/components/SearchResultPagination";

describe("SearchResultPagination", () => {
  it("Snapshot Test", () => {
    const searchResultPagination = shallow(
      <SearchResultPagination
        totalPageCount={10}
        currentPage={1}
        handlePageChange={jest.fn()}
      />
    );
    expect(searchResultPagination).toMatchSnapshot();
  });
});
