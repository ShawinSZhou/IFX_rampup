import { ProductDetails } from "../ProductDetailTab/ProductDetails";

export interface ProductDetailInputProps {
  productDetail: ProductDetails;
  onInputChange: (field: keyof ProductDetails, value: string | number) => void;
  index: number;
}
