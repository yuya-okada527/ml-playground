import React from "react";
import { shallow } from "enzyme";
import SideBar from "../src/components/SideBar";

describe("SideBar", () => {
  it("Shapshot Test", () => {
    const sideBar = shallow(<SideBar />);
    expect(sideBar).toMatchSnapshot();
  });
});
