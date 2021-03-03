import React from "react";
import { shallow } from "enzyme";
import MetaData from "../src/components/MetaData";

describe("MetaData", () => {
  it("Snapshot Test", () => {
    const metaData = shallow(<MetaData title={"title"} />);
    expect(metaData).toMatchSnapshot();
  });
});
