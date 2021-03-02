import React from "react";
import { shallow } from "enzyme";
import ProviderInfo from "../src/components/ProviderInfo";

describe("ProviderInfo", () => {
  it("Snapshot Test", () => {
    const providerInfo = shallow(<ProviderInfo />);
    expect(providerInfo).toMatchSnapshot();
  });
});
