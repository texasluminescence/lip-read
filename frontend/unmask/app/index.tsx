import { Text, View } from "react-native";
import Body from "@/components/Body";

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Body />
    </View>
  );
}