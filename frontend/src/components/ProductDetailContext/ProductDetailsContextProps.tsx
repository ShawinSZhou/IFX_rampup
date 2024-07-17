import { ProductDetails } from "../ProductDetailTab/ProductDetails";

// Define the structure of product details
// Define the context's value structure
export interface ProductDetailsContextProps {

  productDetailsList: ProductDetails[];
  
  updateProductDetails: (
    index: number,
    field: keyof ProductDetails,
    value: any
  ) => void;
  // updateProductDetails 是一个函数，用于更新 productDetailsList 中的元素。
  // 接收三个参数：index（数组中元素的位置），field（ProductDetails 类型中的键名），以及 value（新的值）。
}
