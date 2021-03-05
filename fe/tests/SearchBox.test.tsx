import React from "react";
import { shallow } from "enzyme";
import SearchBox from "../src/components/SearchBox";

describe("SearchBox", () => {
  it("Snapshot Test", () => {
    const searchBox = shallow(
      <SearchBox
        searchTerm="searchTerm"
        handleSearchTermChange={jest.fn()}
        handleSearchButtonClick={jest.fn()}
      />
    );
    expect(searchBox).toMatchSnapshot();
  });
});
