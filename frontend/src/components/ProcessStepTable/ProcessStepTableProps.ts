import { ProductDetails } from "../ProductDetailTab/ProductDetails";
import { DemandData } from "../DemandTable/DemandData";
import { ProcessStepData } from "../ProcessStepTable/ProcessStepData";
export interface ProcessStepTableProps {
   productDetail: ProductDetails;
  onInputChange: (field: keyof ProductDetails, value: string | number|DemandData[]|ProcessStepData[]) => void;
  index: number;
}
