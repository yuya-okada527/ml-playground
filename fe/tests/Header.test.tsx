import React from "react";
import { shallow } from "enzyme";
import Header from "../src/components/Header";

describe("Header", () => {
  it("Snapshot Test", () => {
    const header = shallow(<Header />);
    expect(header).toMatchSnapshot();
  });
});
