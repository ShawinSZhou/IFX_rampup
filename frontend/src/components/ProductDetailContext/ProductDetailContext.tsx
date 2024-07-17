// ProductDetailsContext.tsx
import React, { createContext, useState, useContext } from "react";

import { ProductDetails } from "../ProductDetailTab/ProductDetails";
import { ProductDetailsContextProps } from "./ProductDetailsContextProps";

// Create the context
const ProductDetailsContext = createContext<ProductDetailsContextProps>({
  productDetailsList: [],
  updateProductDetails: () => {},
});

// Export the context's hook
export const useProductDetails = () => useContext(ProductDetailsContext);

export const defaultProductDetails: ProductDetails = {
  salesCode: "",
  basicType: "",
  tBase: 0,
  parallelity: 0,
  chipPerWafer: 0,
  reachLevel: 0,
  stockBuffer: 0,
  ORTLevel: 0,
  reworkPercentage: 0,
  demandData: [],
  processStepData: [
    { step: "FE", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "bumping", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "sort", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "DPS", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "DC", cycleTime: 0, transitTime: 0, yield: 0 },
  ],
};

// Define the context provider component
export const ProductDetailsProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const [productDetailsList, setProductDetailsList] = useState<
    ProductDetails[]
  >([defaultProductDetails]);

  // Function to update an individual product's details
  const updateProductDetails = (
    index: number,
    field: keyof ProductDetails,
    value: any
  ) => {
    setProductDetailsList((currentList) => {
      const newList = [...currentList];
      const updatedDetails = { ...newList[index], [field]: value };
      newList[index] = updatedDetails;
      return newList;
    });
  };

  // Provide the state and updater function to the context
  return (
    <ProductDetailsContext.Provider
      value={{ productDetailsList, updateProductDetails }}
    >
      {children}
    </ProductDetailsContext.Provider>
  );
};
