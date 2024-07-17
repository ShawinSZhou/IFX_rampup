// ProductTabsManager.tsx
import React, { useState, useEffect } from "react";
import { Box, Tab, Tabs, Button } from "@mui/material";
import { ProductDetailTab } from "../ProductDetailTab/ProductDetailTab";
import { useProductDetails } from "../ProductDetailContext/ProductDetailContext";
import { defaultProductDetails } from "../ProductDetailContext/ProductDetailContext";

export const ProductTabsManager: React.FC = () => {
  const { productDetailsList, updateProductDetails } = useProductDetails();
  const [tabIndex, setTabIndex] = useState<number>(0); // The current active tab index

  // Function to create a new product details object with default values
  const createNewProductDetails = () => ({
    defaultProductDetails,
  });

  const addNewProductDetails = (newIndex: number) => {
    const newProductDetails = createNewProductDetails().defaultProductDetails;

    updateProductDetails(newIndex, "salesCode", newProductDetails.salesCode);
    updateProductDetails(newIndex, "basicType", newProductDetails.basicType);
    updateProductDetails(newIndex, "tBase", newProductDetails.tBase);
    updateProductDetails(
      newIndex,
      "parallelity",
      newProductDetails.parallelity
    );
    updateProductDetails(
      newIndex,
      "chipPerWafer",
      newProductDetails.chipPerWafer
    );
    updateProductDetails(newIndex, "reachLevel", newProductDetails.reachLevel);
    updateProductDetails(
      newIndex,
      "stockBuffer",
      newProductDetails.stockBuffer
    );
    updateProductDetails(newIndex, "ORTLevel", newProductDetails.ORTLevel);
    updateProductDetails(
      newIndex,
      "reworkPercentage",
      newProductDetails.reworkPercentage
    );
    updateProductDetails(newIndex, "demandData", newProductDetails.demandData);
    updateProductDetails(
      newIndex,
      "processStepData",
      newProductDetails.processStepData
    );
  };

  // Initialize the first tab on component mount
  useEffect(() => {
    if (productDetailsList.length === 0) {
      addNewProductDetails(0);
    }
  }, []); // Only run once on mount

  const handleAddTab = () => {
    const newIndex = productDetailsList.length;
    addNewProductDetails(newIndex);
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
    console.log(productDetailsList);
  };

  interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
  }

  function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`tabpanel-${index}`}
        aria-labelledby={`tab-${index}`}
        {...other}
      >
        {value === index && <Box p={3}>{children}</Box>}
      </div>
    );
  }

  return (
    <Box>
      <Tabs
        value={tabIndex}
        onChange={handleTabChange}
        aria-label="product details tabs"
      >
        {productDetailsList.map((_, index) => (
          <Tab key={index} label={`Product ${index + 1}`} />
        ))}
      </Tabs>
      <Button onClick={handleAddTab}>+ Add new product</Button>
      {productDetailsList.map((_, index) => (
        <TabPanel key={index} value={tabIndex} index={index}>
          <ProductDetailTab index={index} />
        </TabPanel>
      ))}
    </Box>
  );
};
