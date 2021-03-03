import React from "react";
import { shallow } from "enzyme";
import Footer from "../src/components/Footer";

describe("Footer", () => {
  it("Snapshot Test", () => {
    const footer = shallow(<Footer />);
    expect(footer).toMatchSnapshot();
  });
});
