import { ProductDetails } from "../ProductDetailTab/ProductDetails";
import { DemandData } from "./DemandData";
import { ProcessStepData } from "../ProcessStepTable/ProcessStepData";
export interface DemandTableProps {
  productDetail: ProductDetails;
  onInputChange: (field: keyof ProductDetails, value: string | number|DemandData[]|ProcessStepData[]) => void;
  index: number;
}
