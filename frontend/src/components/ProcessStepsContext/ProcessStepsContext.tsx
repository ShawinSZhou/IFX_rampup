// ProcessStepsContext.tsx
import React, { createContext, useState, useContext } from "react";

interface FormValues {
  step: string;
  cycleTime: string;
  transitTime: string;
  yield: string;
}

interface ProcessStepsContextProps {
  formValues: FormValues[];
  setFormValues: React.Dispatch<React.SetStateAction<FormValues[]>>;
}

const ProcessStepsContext = createContext<ProcessStepsContextProps | null>(
  null
);

export const useProcessSteps = () => useContext(ProcessStepsContext)!;

export const ProcessStepsProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const typeOfProcessStep = ["FE", "bumping", "sort", "DPS", "DC"];
  const initialFormValues: FormValues[] = typeOfProcessStep.map((step) => ({
    step,
    cycleTime: "",
    transitTime: "",
    yield: "",
  }));

  const [formValues, setFormValues] = useState<FormValues[]>(initialFormValues);

  return (
    <ProcessStepsContext.Provider value={{ formValues, setFormValues }}>
      {children}
    </ProcessStepsContext.Provider>
  );
};
