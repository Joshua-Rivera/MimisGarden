import { useEffect, useState } from "react";

const PHONE_SHORT_SIDE_MAX = 699;

const getIsPhone = () =>
  typeof window !== "undefined" &&
  Math.min(window.innerWidth, window.innerHeight) <= PHONE_SHORT_SIDE_MAX;

/**
 * Classifies phones by the viewport's shorter side so the result does not
 * change when the same device rotates between portrait and landscape.
 */
export default function useIsPhone() {
  const [isPhone, setIsPhone] = useState(getIsPhone);

  useEffect(() => {
    const updateDevice = () => setIsPhone(getIsPhone());

    window.addEventListener("resize", updateDevice);
    window.addEventListener("orientationchange", updateDevice);
    return () => {
      window.removeEventListener("resize", updateDevice);
      window.removeEventListener("orientationchange", updateDevice);
    };
  }, []);

  return isPhone;
}
