import { Box, Stack } from "@mui/material";

import { ProcessStepTable } from "../ProcessStepTable/ProcessStepTable";
import { DemandTable } from "../DemandTable/DemandTable";
import { DemandData } from "../DemandTable/DemandData";
import { ProcessStepData } from "../ProcessStepTable/ProcessStepData";

import { useProductDetails } from "../ProductDetailContext/ProductDetailContext";
import { ProductDetailInput } from "../ProductDetailInput/ProductDetailInput";
import { ProductDetails } from "./ProductDetails";


export function ProductDetailTab({ index }: { index: number }) {
  const { productDetailsList, updateProductDetails } = useProductDetails();
  // 使用 useProductDetails 钩子获取产品详细信息列表和更新函数。
  const handleInputChange = (
    field: keyof ProductDetails,
    value: string | number | DemandData[] | ProcessStepData[]
  ) => {
    // 定义一个函数 handleInputChange，用来处理输入变化。
    // 它接受一个 ProductDetails 类型的键名和一个可能是字符串、数字、DemandData数组或ProcessStepData数组类型的值。
    
    if (productDetailsList[index]) {
      updateProductDetails(index, field, value);
    }
    // Ensure the product detail exists before trying to update it
  };

  return (
    <Box display="flex" alignItems="center" justifyContent="center">
      <Stack spacing={5}>
        <ProductDetailInput
          productDetail={productDetailsList[index]}
          onInputChange={handleInputChange}
          index={index}
        />
        {/* 使用 ProductDetailInput 组件，传递产品详情、处理函数和索引 */}
        
        <DemandTable
          productDetail={productDetailsList[index]}
          onInputChange={handleInputChange}
          index={index}
        />
        <ProcessStepTable
          productDetail={productDetailsList[index]}
          onInputChange={handleInputChange}
          index={index}
        />
      </Stack>
    </Box>
  );
}
